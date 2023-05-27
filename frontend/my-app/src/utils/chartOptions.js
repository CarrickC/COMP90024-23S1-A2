/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

import { toJS } from "mobx";

const getChartOptions = (type, dataStore) => {
  const mapOption = {
    tooltip: {
      trigger: "item",
      showDelay: 0,
      transitionDuration: 0.2,
    },
  };

  if (type === "avgToxMap") {
    mapOption.visualMap = {
      left: "right",
      min: 0,
      max: 1,
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
      show: true,
    };
    mapOption.series = [
      {
        name: "Toxicity",
        type: "map",
        roam: true,
        map: "melb",
        emphasis: {
          label: {
            show: false,
          },
        },
        data: dataStore.getData(type),
      },
    ];

    return mapOption;
  } else if (type === "locToxMap") {
    mapOption.visualMap = {
      left: "right",
      min: 0,
      max: 1,
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
      show: true,
    };
    mapOption.series = [
      {
        name: "Toxicity",
        type: "map",
        roam: true,
        map: "melb",
        emphasis: {
          label: {
            show: false,
          },
        },
        data: dataStore.getData(type),
      },
    ];

    return mapOption;
  } else if (type === "avgSentMap") {
    mapOption.visualMap = {
      left: "right",
      min: 0,
      max: 1,
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
      show: true,
    };
    mapOption.series = [
      {
        name: "Sentiment Probability",
        type: "map",
        roam: true,
        map: "melb",
        emphasis: {
          label: {
            show: false,
          },
        },
        data: dataStore.getData(type),
      },
    ];

    return mapOption;
  } else if (type === "locSentMap") {
    mapOption.visualMap = {
      left: "right",
      min: 0,
      max: 1,
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
      show: true,
    };
    mapOption.series = [
      {
        name: "",
        type: "map",
        roam: true,
        map: "melb",
        emphasis: {
          label: {
            show: false,
          },
        },
        data: dataStore.getData(type),
      },
    ];

    return mapOption;
  } else if (type === "statMap") {
    const min = dataStore.statType === "rent" ? 200 : 100;
    const max = dataStore.statType === "rent" ? 600 : 5000;
    mapOption.visualMap = {
      left: "right",
      min: min,
      max: max,
      precision: 0,
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
      show: true,
    };
    mapOption.series = [
      {
        name: "",
        type: "map",
        roam: true,
        map: "melb",
        emphasis: {
          label: {
            show: false,
          },
        },
        data: dataStore.getData(type),
      },
    ];

    return mapOption;
  } else if (type === "twWordCntBar") {
    return {
      tooltip: {},
      dataset: {
        dimensions: ["name", "value"],
        source: dataStore.getData(type),
      },
      xAxis: {},
      yAxis: { type: "category", inverse: true },
      series: [{ type: "bar" }],
      grid: {
        top: 10,
        bottom: 20,
        right: 100,
        containLabel: true,
      },
      dataZoom: [
        {
          show: true,
          type: "slider",
          realtime: true,
          maxValueSpan: 16,
          handleSize: "200%",
          width: 20,
          yAxisIndex: [0],
          showDetail: false,
        },
        {
          type: "inside",
          start: 0,
          end: 0.05,
          zoomOnMouseWheel: false,
          moveOnMouseWheel: true,
          moveOnMouseMove: true,
          yAxisIndex: [0],
        },
      ],
    };
  } else if (type === "mdWordCntBar") {
    return {
      tooltip: {},
      dataset: {
        dimensions: ["name", "value"],
        source: dataStore.getData(type),
      },
      xAxis: {},
      yAxis: { type: "category", inverse: true },
      series: [{ type: "bar" }],
      grid: {
        top: 10,
        bottom: 20,
        right: 100,
        containLabel: true,
      },
      dataZoom: [
        {
          show: true,
          type: "slider",
          realtime: true,
          maxValueSpan: 16,
          handleSize: "200%",
          width: 20,
          yAxisIndex: [0],
          showDetail: false,
        },
        {
          type: "inside",
          start: 0,
          end: 0.05,
          zoomOnMouseWheel: false,
          moveOnMouseWheel: true,
          moveOnMouseMove: true,
          yAxisIndex: [0],
        },
      ],
    };
  } else if (type === "twSentDistPie") {
    return {
      tooltip: {
        trigger: "item",
      },
      series: [
        {
          name: "Access From",
          type: "pie",
          radius: "50%",
          data: dataStore.getData(type),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
          },
        },
      ],
    };
  } else if (type === "mdSentDistPie") {
    return {
      tooltip: {
        trigger: "item",
      },
      series: [
        {
          name: "Access From",
          type: "pie",
          radius: "50%",
          data: dataStore.getData(type),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
          },
        },
      ],
    };
  } else if (type === "fllrScatter") {
    return {
      visualMap: {
        min: 0,
        max: 1,
        dimension: 1,
        orient: "vertical",
        right: 10,
        top: "center",
        text: ["HIGH", "LOW"],
        calculable: true,
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
        show: false,
      },
      tooltip: {
        trigger: "item",
        axisPointer: { type: "cross" },
      },
      xAxis: [
        {
          type: "value",
          name: "#followers",
          nameLocation: "middle",
          nameGap: 30,
        },
      ],
      yAxis: [
        {
          type: "value",
          name: "toxicity",
          nameLocation: "middle",
          nameGap: 30,
        },
      ],
      series: [
        {
          name: "",
          type: "scatter",
          symbolSize: 5,
          data: dataStore.getData(type).data,
        },
        {
          name: "",
          type: "line",
          data: dataStore.getData(type).avgs,
          lineStyle: {
            normal: {
              color: "orange",
              width: 5,
            },
          },
        },
      ],
    };
  } else if (type === "fllgScatter") {
    return {
      visualMap: {
        min: 0,
        max: 1,
        dimension: 1,
        orient: "vertical",
        right: 10,
        top: "center",
        text: ["HIGH", "LOW"],
        calculable: true,
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
        show: false,
      },
      tooltip: {
        trigger: "item",
        axisPointer: { type: "cross" },
      },
      xAxis: [
        {
          type: "value",
          name: "#following",
          nameLocation: "middle",
          nameGap: 30,
        },
      ],
      yAxis: [
        {
          type: "value",
          name: "toxicity",
          nameLocation: "middle",
          nameGap: 30,
        },
      ],
      series: [
        {
          name: "",
          type: "scatter",
          symbolSize: 5,
          data: dataStore.getData(type).data,
        },
        {
          name: "",
          type: "line",
          data: dataStore.getData(type).avgs,
          lineStyle: {
            normal: {
              color: "orange",
              width: 5,
            },
          },
        },
      ],
    };
  } else if (type === "popByAgeBar") {
    return {
      tooltip: {},
      legend: {
        orient: "horizontal",
      },
      dataset: {
        dimensions: ["Suburb", "Age 0-19", "Age 20-39", "Age 40-59", "Age 60+"],
        source: dataStore.getData(type),
      },
      xAxis: {
        type: "category",
        axisLabel: { show: true, interval: 0, rotate: 30 },
        splitLine: { show: true },
      },
      yAxis: {},
      series: [
        { type: "bar" },
        { type: "bar" },
        { type: "bar" },
        { type: "bar" },
      ],
      grid: {
        top: 50,
        bottom: 1,
        left: 20,
        right: 20,
        containLabel: true,
      },
    };
  } else if (type === "popByGenderBar") {
    return {
      tooltip: {},
      legend: {
        orient: "horizontal",
      },
      dataset: {
        dimensions: ["Suburb", "Female", "Male"],
        source: dataStore.getData(type),
      },
      xAxis: {
        type: "category",
        axisLabel: { show: true, interval: 0, rotate: 30 },
        splitLine: { show: true },
      },
      yAxis: {},
      series: [{ type: "bar" }, { type: "bar" }],
      grid: {
        top: 50,
        bottom: 1,
        left: 20,
        right: 20,
        containLabel: true,
      },
    };
  } else if (type === "pkSpcBar") {
    return {
      tooltip: {},
      legend: {},
      dataset: {
        dimensions: ["Suburb", "Commercial", "Private", "Residential"],
        source: dataStore.getData(type),
      },
      xAxis: {},
      yAxis: { type: "category", inverse: true },
      series: [{ type: "bar" }, { type: "bar" }, { type: "bar" }],
      grid: {
        top: 30,
        bottom: 20,
        left: 180,
        right: 50,
        // containLabel: true,
      },
      // dataZoom: [
      //   {
      //     show: true,
      //     type: "slider",
      //     realtime: true,
      //     maxValueSpan: 5,
      //     handleSize: "200%",
      //     width: 20,
      //     yAxisIndex: [0],
      //     showDetail: false,
      //   },
      //   {
      //     type: "inside",
      //     start: 0,
      //     end: 0.05,
      //     zoomOnMouseWheel: false,
      //     moveOnMouseWheel: true,
      //     moveOnMouseMove: true,
      //     yAxisIndex: [0],
      //   },
      // ],
    };
  } else if (type === "patronBar") {
    return {
      tooltip: {},
      dataset: {
        dimensions: ["Suburb", "Patrons"],
        source: dataStore.getData(type),
      },
      xAxis: {},
      yAxis: { type: "category", inverse: true },
      series: [{ type: "bar", barWidth: 20 }],
      grid: {
        top: 10,
        bottom: 20,
        left: 180,
        right: 50,
        // containLabel: true,
      },
      // dataZoom: [
      //   {
      //     show: true,
      //     type: "slider",
      //     realtime: true,
      //     maxValueSpan: 5,
      //     handleSize: "200%",
      //     width: 20,
      //     yAxisIndex: [0],
      //     showDetail: false,
      //   },
      //   {
      //     type: "inside",
      //     start: 0,
      //     end: 0.05,
      //     zoomOnMouseWheel: false,
      //     moveOnMouseWheel: true,
      //     moveOnMouseMove: true,
      //     yAxisIndex: [0],
      //   },
      // ],
    };
  } else if (type === "jobBar") {
    return {
      tooltip: {},
      dataset: {
        dimensions: ["Suburb", "Jobs"],
        source: dataStore.getData(type),
      },
      xAxis: {},
      yAxis: { type: "category", inverse: true },
      series: [{ type: "bar", barWidth: 20 }],
      grid: {
        top: 10,
        bottom: 20,
        left: 180,
        right: 50,
        // containLabel: true,
      },
      // dataZoom: [
      //   {
      //     show: true,
      //     type: "slider",
      //     realtime: true,
      //     maxValueSpan: 5,
      //     handleSize: "200%",
      //     width: 20,
      //     yAxisIndex: [0],
      //     showDetail: false,
      //   },
      //   {
      //     type: "inside",
      //     start: 0,
      //     end: 0.05,
      //     zoomOnMouseWheel: false,
      //     moveOnMouseWheel: true,
      //     moveOnMouseMove: true,
      //     yAxisIndex: [0],
      //   },
      // ],
    };
  }
};

export default getChartOptions;
