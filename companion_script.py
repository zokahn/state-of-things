
import argparse
import requests

def create_project(api_url, api_token, project_name, project_description):
    headers = {'Authorization': 'Bearer ' + api_token}
    data = {'name': project_name, 'description': project_description}
    response = requests.post(api_url + '/projects/', json=data, headers=headers)
    return response.json() if response.status_code == 200 else None

def read_mode(api_url, api_token, project_id):
    headers = {'Authorization': 'Bearer ' + api_token}
    response = requests.get(api_url + '/projects/' + project_id, headers=headers)
    if response.status_code == 200:
        project = response.json()
        print(f"Project: {project['name']}\nDescription: {project['description']}")
    else:
        print(f"Failed to fetch project details. Status code: {response.status_code}")

def write_mode(api_url, api_token, project_id):
    entity_type = input('Enter entity type: ')
    name = input('Enter name: ')
    description = input('Enter description: ')
    data = {'name': name, 'description': description, 'project_id': project_id}
    response = requests.post(f"{api_url}/{entity_type}s/", json=data, headers={'Authorization': 'Bearer ' + api_token})
    print(f"{entity_type.capitalize()} added successfully." if response.status_code == 200 else f"Failed to add {entity_type}.")

def main():
    parser = argparse.ArgumentParser(description='Project Management API Companion')
    parser.add_argument('mode', choices=['read', 'write'])
    parser.add_argument('--url', required=True)
    parser.add_argument('--token', required=True)
    parser.add_argument('--project', required=True)
    args = parser.parse_args()
    if args.mode == 'read':
        read_mode(args.url, args.token, args.project)
    elif args.mode == 'write':
        write_mode(args.url, args.token, args.project)

if __name__ == '__main__':
    main()
