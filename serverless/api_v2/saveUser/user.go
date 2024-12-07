package main

import (
	"context"
	"os"

	firebase "firebase.google.com/go"
	"firebase.google.com/go/db"
	"google.golang.org/api/option"
)

type User struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

func (u User) findById(id string) (*User, error) {
	ref, ctx, err := u.useRef()
	if err != nil {
		return nil, err
	}

	results, err := ref.OrderByChild("id").EqualTo(id).LimitToFirst(1).GetOrdered(ctx)
	if err != nil || len(results) == 0 {
		return nil, err
	}

	var user User
	if err := results[0].Unmarshal(&user); err != nil {
		return nil, err
	}
	return &user, nil
}

func (u User) save() error {
	ref, ctx, err := u.useRef()
	if err != nil {
		return err
	}

	if err := ref.Child(u.ID).Set(ctx, &u); err != nil {
		return err
	}
	return nil
}

func (u User) useRef() (*db.Ref, context.Context, error) {
	var ref *db.Ref
	ctx := context.Background()

	conf := &firebase.Config{DatabaseURL: os.Getenv("FIREBASE_DATABASE_URL")}
	opt := option.WithCredentialsFile(os.Getenv("FIREBASE_SERVICE_KEY"))
	app, err := firebase.NewApp(ctx, conf, opt)
	if err != nil {
		return ref, ctx, err
	}

	client, err := app.Database(ctx)
	if err != nil {
		return ref, ctx, err
	}

	ref = client.NewRef("users")
	return ref, ctx, nil
}
