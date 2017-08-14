# python simple app
This is a simple python REST application using Tornado & MongoDB.<br>
To run this simply replace the user&pwd for the DB connection string under config.py and run application.py

You can use Postman to test the API

![desktop 1_010](https://user-images.githubusercontent.com/30981317/29260887-4342dd30-80d5-11e7-94e1-b5c242718b35.png)

Get users is implemented with Tornado asynchronous as an async call <br>
The below screen shows how the "get" request is running in the backround while a new user is created in another request.

![selection_011](https://user-images.githubusercontent.com/30981317/29261162-d460e2c0-80d6-11e7-9590-ae9db7c39019.png)

# Testing

The testing has it's own application defined, with specific database configuration that is deleted on every run. <br>
To run the tests simply run test_sample.py or use the command python -m unittest test_sample.TestUsersHandler

![selection_013](https://user-images.githubusercontent.com/30981317/29261438-223fa37c-80d8-11e7-9eb3-8ecff554de16.png)

![selection_016](https://user-images.githubusercontent.com/30981317/29261586-f0f451d6-80d8-11e7-8b48-63f787a04026.png)
