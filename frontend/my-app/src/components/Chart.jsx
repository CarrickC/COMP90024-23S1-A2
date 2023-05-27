/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

// import React from "react";
import { Card, Col, Spin } from "antd";
import * as echarts from "echarts";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import Map from "./Map";
import React from "react";
import { getChartOptions } from "@/utils";
import { useStore } from "@/stores";
import { observer } from "mobx-react-lite";

const Chart = observer(({ chartTitle, chartType }) => {
  let chartInstance = null;

  const { dataStore } = useStore();

  const chartRef = useRef(null);

  const fetchData = dataStore.getFetchData(chartType);

  const initChart = () => {
    chartInstance = echarts.getInstanceByDom(chartRef.current);

    if (!chartInstance) {
      chartInstance = echarts.init(chartRef.current);
      let timer = null;
      const resizeObserver = new ResizeObserver(() => {
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
          chartInstance.resize();
        }, 100);
      });
      resizeObserver.observe(chartRef.current);
    }
  };

  const updateChart = () => {
    chartInstance = echarts.getInstanceByDom(chartRef.current);
    chartInstance.setOption(getChartOptions(chartType, dataStore));
  };

  useEffect(() => {
    initChart();

    if (!dataStore.isDataLoaded(chartType)) {
      fetchData().then(() => {
        updateChart();
        dataStore.setDataLoaded(chartType, true);
      });
    } else {
      dataStore.setDataLoaded(chartType, false);
      setTimeout(() => {
        updateChart();
        dataStore.setDataLoaded(chartType, true);
      }, 300);
    }

    const cleanup = () => {
      if (chartInstance) {
        chartInstance.dispose();
      }
    };

    return cleanup;
  }, []);

  return (
    <Card title={chartTitle}>
      <Spin spinning={!dataStore.isDataLoaded(chartType)}>
        <div ref={chartRef} style={{ height: "600px" }} />
      </Spin>
    </Card>
  );
});

export default Chart;
