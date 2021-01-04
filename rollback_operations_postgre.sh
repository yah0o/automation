#! /bin/bash

PERIOD="7 days"
ENTITY_CODE=""
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
  -h | --dbhost)
    DB_HOST="$2"
    shift
    shift
    ;;
  -u | --dbuser)
    DB_USER="$2"
    shift
    shift
    ;;
  -i | --service)
    SERVICE_HOST="$2"
    shift
    shift
    ;;
  -n | --namespace)
    NAMESPACE="$2"
    shift
    shift
    ;;
  -p | --period)
    PERIOD="$2"
    shift
    shift
    ;;
  -e | --entity-code)
    ENTITY_CODE="$2"
    shift
    shift
    ;;
  -d | --dry-run)
    DRYRUN=true
    shift
    ;;
  *)
    POSITIONAL+=("$1")
    shift
    ;;
  esac
done
set -- "${POSITIONAL[@]}"

if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$SERVICE_HOST" ] || [ -z "$NAMESPACE" ]; then
  echo "Usage:"
  echo "  ./rollback_operations.sh -h <DB_HOST> -u <DB_USER> -i <SERVICE_HOST> -n <NAMESPACE> -e <ENTITY_CODE> -p '<PERIOD>' [-d|--dry-run]"
  exit 1
fi

if [ -z "$ENTITY_CODE" ]; then
  echo "Querying DB to get pending transactions"
  query_output=$(
    psql -t -A -F"," -h $DB_HOST -p 5432 -U $DB_USER <<END
select et.id, et.root_external_id, eti.ENTITY_CODE
from entity_transaction et join entity_transaction_item eti on et.id = eti.transaction_id
where transaction_status = 0
  AND namespace in ('$NAMESPACE')
  AND create_date < 'now'::timestamp - '6 hour'::interval AND create_date > 'now'::timestamp - '$PERIOD'::interval
  AND (hold_amount > 0 OR grant_amount > 0)
  order by et.create_date ASC;
END
  )
else
  echo "Querying DB to get pending transactions by entity"
  query_output=$(
    psql -t -A -F"," -h $DB_HOST -p 5432 -U $DB_USER <<END
select et.id, et.root_external_id, eti.ENTITY_CODE
from entity_transaction et join entity_transaction_item eti on et.id = eti.transaction_id
where transaction_status = 0
  AND namespace in ('$NAMESPACE')
  AND ENTITY_CODE in ('$ENTITY_CODE')
  AND create_date < 'now'::timestamp - '6 hour'::interval AND create_date > 'now'::timestamp - '$PERIOD'::interval
  AND (hold_amount > 0 OR grant_amount > 0)
  order by et.create_date ASC;
END
  )
fi

if [ -z "$DRYRUN" ]; then
  echo "$query_output" | while IFS="," read transaction_id user_id ENTITY_CODE; do
    if [ ! -z "$transaction_id" ]; then
      echo ".Rolling back transaction $transaction_id for user $user_id and entity $ENTITY_CODE"
      curl -X POST \
        "http://$SERVICE_HOST/entity/api/v3/$NAMESPACE/root/$user_id/$user_id/rollback/$transaction_id" \
        -H 'Content-Type: application/json' \
        -d '{}'
    fi
  done
else
  echo "Rollback skipped:"
  echo "$query_output"
fi