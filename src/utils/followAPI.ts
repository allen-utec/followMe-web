import type {
  ILocation,
  ILocationPayload,
  IRoutePayload,
  IUser,
} from "./types";

export async function saveUser(payload: IUser) {
  return fetch(`${import.meta.env.VITE_FOLLOWME_API}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then((res) => {
    if (!res.ok) throw new Error(res.statusText);
  });
}

export async function postLocation(payload: ILocationPayload) {
  return fetch(`${import.meta.env.VITE_FOLLOWME_API}/locations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then((res) => {
    if (!res.ok) throw new Error(res.statusText);
  });
}

export async function postRoute(payload: IRoutePayload) {
  return fetch(`${import.meta.env.VITE_FOLLOWME_API}/routes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).then((res) => {
    if (!res.ok) throw new Error(res.statusText);
  });
}

export async function getRoute(tenantId: string, routeId: string) {
  return fetch(
    `${import.meta.env.VITE_FOLLOWME_API}/locations/${tenantId}/${routeId}`
  )
    .then<{ data: ILocation[] }>((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then(({ data }) => data.sort((a, b) => a.timestamp - b.timestamp));
}
