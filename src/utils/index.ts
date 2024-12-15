import { nanoid } from "nanoid";
import type { IUser } from "./types";

export function getUser() {
  let user: IUser;
  let userStr = localStorage.getItem("user");

  if (!userStr) {
    user = { id: nanoid(10), name: "incognito" };
    localStorage.setItem("user", JSON.stringify(user));
  } else {
    user = JSON.parse(userStr);
  }

  return user;
}

export function getRouteId() {
  return nanoid();
}

export function diffInMinutes(timestamp?: number) {
  if (!timestamp) {
    return 0;
  }
  const diffMinutes = Math.ceil(Math.abs(Date.now() - timestamp) / 1000 / 60);
  return diffMinutes;
}
