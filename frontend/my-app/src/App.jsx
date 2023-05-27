/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "@/pages/MainLayout";
import Sentiment from "@/pages/Sentiment";
import Toxicity from "@/pages/Toxicity";
import Statistic from "./pages/Statistic";
import { observer } from "mobx-react-lite";
import Suburb from "./pages/Statistic";

import "./App.css";

const App = () => {
  return (
    <BrowserRouter>
      <div>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Toxicity />} />
            <Route path="sentiment" element={<Sentiment />} />
            <Route path="statistic" element={<Statistic />} />
          </Route>
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
