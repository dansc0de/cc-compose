#!/bin/bash
# test_endpoints.sh
# This script tests all endpoints of the FastAPI tasks server:
#  1. Create a task
#  2. Get the list of tasks
#  3. Update the task
#  4. Delete the task
#
# Prerequisites:
#   - The server is running on http://localhost:8000
#   - 'curl' is installed
#   - 'jq' is installed (for parsing JSON responses)

BASE_URL="http://localhost"

check_status() {
    local status_code=$1
    local operation=$2
    if [[ "$status_code" -ne 200 && "$status_code" -ne 201 ]]; then
        echo "Error: $operation failed with status code $status_code"
        exit 1
    fi
}

generate_post_data() {
    cat <<EOF
{
  "title": "GHA Task",
  "description": "This is a test task for GHA CI",
  "completed": false
}
EOF
}

echo "#### Generate a new task ####"
post_response=$(curl -s -o response.json -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$(generate_post_data)" $BASE_URL/api/tasks)
check_status "$post_response" "POST /api/tasks"
printf "\n"
cat response.json
printf "\n"

task_id=$(jq -r '.id' response.json)
echo "Task ID: $task_id"


echo "#### Get the list of tasks ####"
get_response=$(curl -s -o response.json -w "%{http_code}" $BASE_URL/api/tasks)
check_status "$get_response" "GET /api/tasks"
printf "\n"
cat response.json
printf "\n"


echo "#### Update the task ####"
update_response=$(curl -s -o response.json -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d '{"title": "GHA Task Updated"}' $BASE_URL/api/tasks/$task_id)
check_status "$update_response" "PUT /api/tasks/$task_id"
printf "\n"
cat response.json
printf "\n"


echo "#### Delete the task ####"
delete_response=$(curl -s -o response.json -w "%{http_code}" -X DELETE $BASE_URL/api/tasks/$task_id)
check_status "$delete_response" "DELETE /api/tasks/$task_id"
printf "\n"
cat response.json
printf "\n"

rm -f response.json
