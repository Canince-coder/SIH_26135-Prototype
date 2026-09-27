import client from "./client";

export const getMyTraineeProfile = () =>
  client.get("/trainees/me").then((r) => r.data);

export const updateMyTraineeProfile = (payload) =>
  client.put("/trainees/me", payload).then((r) => r.data);

export const getMySkills = () =>
  client.get("/trainees/me/skills").then((r) => r.data);

export const addMySkill = (payload) =>
  client.post("/trainees/me/skills", payload).then((r) => r.data);

export const getRecommendedJobs = (limit = 10) =>
  client.get("/trainees/me/recommended-jobs", { params: { limit } }).then((r) => r.data);
