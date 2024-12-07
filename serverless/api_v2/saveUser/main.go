package main

import (
	"context"
	"encoding/json"
	"os"

	firebase "firebase.google.com/go"
	"firebase.google.com/go/db"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"google.golang.org/api/option"
)

type User struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

func Handler(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	ctx := context.Background()

	var user User
	if err := json.Unmarshal([]byte(request.Body), &user); err != nil {
		return errorResponse(err), nil
	}

	userRef, err := usersRef(ctx)
	if err != nil {
		return errorResponse(err), nil
	}

	results, err := userRef.OrderByChild("id").EqualTo(user.ID).LimitToFirst(1).GetOrdered(ctx)
	if err != nil {
		return errorResponse(err), nil
	}

	if len(results) == 0 {
		if err := userRef.Child(user.ID).Set(ctx, &user); err != nil {
			return errorResponse(err), nil
		}
	} else if err := results[0].Unmarshal(&user); err != nil {
		return errorResponse(err), nil
	}

	response, err := json.Marshal(&user)
	if err != nil {
		return errorResponse(err), nil
	}

	return events.APIGatewayProxyResponse{Body: string(response), StatusCode: 201}, nil
}

func main() {
	lambda.Start(Handler)
}

func usersRef(ctx context.Context) (*db.Ref, error) {
	var ref *db.Ref

	conf := &firebase.Config{DatabaseURL: os.Getenv("FIREBASE_DATABASE_URL")}
	opt := option.WithCredentialsFile(os.Getenv("FIREBASE_SERVICE_KEY"))
	app, err := firebase.NewApp(ctx, conf, opt)
	if err != nil {
		return ref, err
	}

	client, err := app.Database(ctx)
	if err != nil {
		return ref, err
	}

	ref = client.NewRef("users")
	return ref, nil
}

type ErrorResponse struct {
	Message string `json:"message"`
}

func errorResponse(err error) events.APIGatewayProxyResponse {
	res, _ := json.Marshal(&ErrorResponse{
		Message: err.Error(),
	})
	return events.APIGatewayProxyResponse{Body: string(res), StatusCode: 500}
}
