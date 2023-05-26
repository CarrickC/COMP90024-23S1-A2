// @ts-nocheck
import React, { useEffect, useRef, useState } from "react";
import * as echarts from "echarts";

import { Row, Col, Card, Spin, Button } from "antd";
import { SyncOutlined } from "@ant-design/icons";

import { useStore } from "../stores";
import { observer } from "mobx-react-lite";
import { action, autorun, computed } from "mobx";

import MapForm from "./MapForm";
import Global from "./Global";
import { getChartOptions } from "@/utils";

const Map = observer((props) => {
  let mapInstance = null;
  const mapRef = useRef(null);
  const { dataStore } = useStore();
  const [loading, setLoading] = useState(false);

  const fetchData = dataStore.getFetchData(props.mapType);
  // const setDataLoaded = dataStore.getSetDataLoaded(props.mapType);
  // const isDataLoaded = dataStore.getIsDataLoaded(props.mapType);

  const initMap = () => {
    mapInstance = echarts.getInstanceByDom(mapRef.current);
    if (!mapInstance) {
      mapInstance = echarts.init(mapRef.current);
      let timer = null;
      const resizeObserver = new ResizeObserver(() => {
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
          mapInstance.resize();
        }, 100);
      });
      resizeObserver.observe(mapRef.current);
    }
  };

  const updateMap = () => {
    mapInstance = echarts.getInstanceByDom(mapRef.current);
    mapInstance.setOption(getChartOptions(props.mapType, dataStore));
  };

  useEffect(() => {
    console.log("init effect call");
    initMap();
    if (!dataStore.isMapLoaded) {
      // setLoading(true);
      // console.log("set loading true");
      dataStore.fetchMap().then(() => {
        dataStore.setMapLoaded(true);
        echarts.registerMap("melb", dataStore.melbMap);

        fetchData().then(() => {
          dataStore.setDataLoaded(props.mapType, true);
          updateMap();
          // setLoading(false);
          // console.log("set loading false");
        });
      });

      if (props.mapType === "locToxMap") {
        dataStore.fetchGloToxData();
      } else if (props.mapType === "locSentMap") {
        dataStore.fetchGloSentData();
      }
    } else {
      if (!dataStore.isDataLoaded(props.mapType)) {
        fetchData().then(() => {
          updateMap();
          dataStore.setDataLoaded(props.mapType, true);
          // setLoading(false)
          // console.log("set loading false");
        });
      } else {
        dataStore.setDataLoaded(props.mapType, false);
        setTimeout(() => {
          updateMap();
          dataStore.setDataLoaded(props.mapType, true);
        }, 500);
      }
    }

    // };

    // load().catch(console.error);

    const cleanUp = () => {
      if (mapInstance) {
        mapInstance.dispose();
      }
    };

    return cleanUp;
  }, []);

  return (
    <Card title={props.mapTitle} style={{ height: "730px" }}>
      <Row gutter={[16, 16]}>
        {props.mapType.substring(0, 3) === "loc" ? (
          <Col span={24}>
            <Global mapType={props.mapType} />
          </Col>
        ) : null}
        <Col span={24}>
          <MapForm formType={props.mapType} updateMap={updateMap} />
        </Col>

        <Col span={24}>
          <Spin spinning={!dataStore.isDataLoaded(props.mapType)}>
            <div ref={mapRef} style={{ height: "500px" }}></div>
          </Spin>
        </Col>
      </Row>
    </Card>
  );
});

export default Map;
