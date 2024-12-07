package main

import (
	"encoding/json"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func Handler(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	var user User
	if err := json.Unmarshal([]byte(request.Body), &user); err != nil {
		return errorResponse(err), nil
	}

	userInDB, err := user.findById(user.ID)
	if err != nil {
		return errorResponse(err), nil
	}

	if userInDB != nil {
		return successResponse(userInDB), nil
	}

	if err := user.save(); err != nil {
		return errorResponse(err), nil
	}

	return successResponse(user), nil
}

func main() {
	lambda.Start(Handler)
}

type ErrorResponse struct {
	Message string `json:"message"`
}

func errorResponse(err error) events.APIGatewayProxyResponse {
	log.Println(err.Error())
	res, _ := json.Marshal(&ErrorResponse{
		Message: "Save user failed",
	})
	return events.APIGatewayProxyResponse{Body: string(res), StatusCode: 400}
}

func successResponse(data interface{}) events.APIGatewayProxyResponse {
	res, _ := json.Marshal(data)
	return events.APIGatewayProxyResponse{Body: string(res), StatusCode: 201}
}
