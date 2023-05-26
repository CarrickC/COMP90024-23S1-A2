import { createContext, useContext } from "react";
import UIStore from "./uiStore";
import DataStore from "./dataStore";

class RootStore {
  constructor() {
    this.dataStore = new DataStore();
    this.uiStore = new UIStore();
  }
}

const rootStore = new RootStore();
const context = createContext(rootStore);
const useStore = () => useContext(context);

export { useStore };
