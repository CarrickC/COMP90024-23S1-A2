import { createContext, useContext } from "react";
import MapStore from "./mapStore";
import UIStore from "./uiStore";

class RootStore {
  constructor() {
    this.mapStore = new MapStore();
    this.uiStore = new UIStore();
  }
}

const rootStore = new RootStore();
const context = createContext(rootStore);
const useStore = () => useContext(context);

export { useStore };
