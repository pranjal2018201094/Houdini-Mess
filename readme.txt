curl  -X POST -d "username=rekha&password=hello" http://127.0.0.1:5000/login

curl  -X POST -d "username=test4&password=foo&age=23&gender=Male&interest=swimming" http://127.0.0.1:5000/register

curl  -X GET  http://127.0.0.1:5000/login

curl  -X GET  http://127.0.0.1:5000/logout

curl  -X GET  http://127.0.0.1:5000/secret_page
