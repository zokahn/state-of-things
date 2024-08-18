import argparse
import requests

def read_mode(api_url, api_token, project_id):
    headers = {'Authorization': 'Bearer ' + api_token}
    response = requests.get(api_url + '/projects/' + project_id, headers=headers)
    if response.status_code == 200:
        project = response.json()
        print('Project:', project['name'])
        print('Description:', project['description'])
        print()
    else:
        print('Failed to fetch project details. Status code:', response.status_code)
        return
    entities = ['tasks', 'issues', 'design_rules', 'requirements', 'project_goals', 'sboms']
    for entity in entities:
        response = requests.get(api_url + '/' + entity + '/?project_id=' + project_id, headers=headers)
        if response.status_code == 200:
            items = response.json()
            print(entity.capitalize() + ':')
            for item in items:
                print('- ' + (item['name'] if 'name' in item else item['title']))
            print()
        else:
            print('Failed to fetch ' + entity + '. Status code:', response.status_code)

def write_mode(api_url, api_token, project_id):
    headers = {'Authorization': 'Bearer ' + api_token}
    entity_type = input('Enter the type of item to add (task, issue, design_rule, requirement, project_goal, sbom): ').lower()
    if entity_type not in ['task', 'issue', 'design_rule', 'requirement', 'project_goal', 'sbom']:
        print('Invalid entity type.')
        return
    name_or_title = input('Enter the name/title of the item: ')
    description = input('Enter the description of the item: ')
    data = {
        'name' if entity_type != 'task' and entity_type != 'issue' else 'title': name_or_title,
        'description': description,
        'project_id': project_id
    }
    response = requests.post(api_url + '/' + entity_type + 's/', json=data, headers=headers)
    if response.status_code == 200:
        print(entity_type.capitalize() + ' added successfully.')
    else:
        print('Failed to add ' + entity_type + '. Status code:', response.status_code)

def main():
    parser = argparse.ArgumentParser(description='Companion script for Project Management API')
    parser.add_argument('mode', choices=['read', 'write'], help='Script mode: read or write')
    parser.add_argument('--url', required=True, help='API URL')
    parser.add_argument('--token', required=True, help='API token')
    parser.add_argument('--project', required=True, help='Project identifier')

    args = parser.parse_args()

    if args.mode == 'read':
        read_mode(args.url, args.token, args.project)
    elif args.mode == 'write':
        write_mode(args.url, args.token, args.project)

if __name__ == '__main__':
    main()
