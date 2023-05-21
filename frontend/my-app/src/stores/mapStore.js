// @ts-nocheck
import { makeAutoObservable } from "mobx";
import * as echarts from "echarts";

class MapStore {
  melbMap = null;

  isLoading = true;

  constructor() {
    makeAutoObservable(this);
  }

  loadMap = () => {
    fetch("http://127.0.0.1:8080/average_toxicity")
      .then((res) => res.json())
      .then((data) => {
        const melbMap = { type: "FeatureCollection", features: [] };
        const melbData = [];
        console.log(data.data);

        Object.entries(data.data).forEach(([key, value]) => {
          melbData.push({ name: key, value: value.average_toxicity });
          melbMap.features.push({
            geometry: value.geometry,
            properties: { name: key },
          });
        });

        console.log(melbMap);
        console.log(melbData);

        echarts.registerMap("USA", melbMap, {
          Alaska: {
            left: -131,
            top: 25,
            width: 15,
          },
          Hawaii: {
            left: -110,
            top: 28,
            width: 5,
          },
          "Puerto Rico": {
            left: -76,
            top: 26,
            width: 2,
          },
        });

        setTimeout(() => {
          let chartInstance = echarts.init(chartRef.current);

          chartInstance.setOption({
            title: {
              text: "Title",
              left: "right",
            },
            tooltip: {
              trigger: "item",
              showDelay: 0,
              transitionDuration: 0.2,
            },
            visualMap: {
              left: "right",
              min: 0,
              max: 0.01,
              inRange: {
                color: [
                  "#313695",
                  "#4575b4",
                  "#74add1",
                  "#abd9e9",
                  "#e0f3f8",
                  "#ffffbf",
                  "#fee090",
                  "#fdae61",
                  "#f46d43",
                  "#d73027",
                  "#a50026",
                ],
              },
              text: ["High", "Low"],
              calculable: true,
            },
            toolbox: {
              show: true,
              //orient: 'vertical',
              left: "left",
              top: "top",
              feature: {
                dataView: { readOnly: false },
                restore: {},
                saveAsImage: {},
              },
            },
            series: [
              {
                name: "USA PopEstimates",
                type: "map",
                roam: true,
                map: "USA",
                emphasis: {
                  label: {
                    show: true,
                  },
                },
                data: melbData,
              },
            ],
          });

          chartInstance.on("finished", function () {
            chartInstance.resize();
          });
        }, 10);
      })
      .catch((e) => {
        console.log(e);
      });
  };
}

export default MapStore;
