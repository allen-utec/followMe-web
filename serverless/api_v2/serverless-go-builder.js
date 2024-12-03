import { spawnSync } from "node:child_process";

export default class GoBuilder {
  constructor() {
    this.hooks = {
      "offline:start:init": () => this.buildGoFunctions(),
    };
  }

  buildGoFunctions() {
    console.log("Building Go functions...");
    spawnSync("make", ["clean", "build"]);
  }
}
