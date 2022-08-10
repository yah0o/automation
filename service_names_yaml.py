import yaml
import xlsxwriter

yamlpath = '~/test.yaml'
realm = 'test'  # yaml name (e.g. yaml for specific environment)

row = 0
column = 0
workbook_name = 'services_{}.xlsx'.format(realm)

with open(yamlpath) as f:
    result =  yaml.load(f, Loader=yaml.Loader)
yaml_entities = list(result.keys())

with xlsxwriter.Workbook(workbook_name) as workbook:
    worksheet = workbook.add_worksheet()

    for data in yaml_entities:
        worksheet.write(row, column, data)
        row += 1

if __name__ == "__main__":
  print('All services are saved in {}'.format(workbook_name))
  print('')
  print(yaml_entities)
  print('')
  print('Amount of yaml entities for yaml={}:'.format(yamlpath), len(yaml_entities))