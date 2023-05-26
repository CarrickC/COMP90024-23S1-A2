import { makeAutoObservable } from "mobx";

class UIStore {
  constructor() {
    makeAutoObservable(this);
  }
}

export default UIStore;
