/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

import React from "react";
import { LikeOutlined } from "@ant-design/icons";
import { Col, Row, Statistic } from "antd";
import { Card } from "antd";
import { observer } from "mobx-react-lite";
import { useStore } from "@/stores";

const Global = observer(({ mapType }) => {
  const { dataStore } = useStore();
  return (
    <Row gutter={0}>
      <Col span={6}>
        <Statistic
          title="Global Moran's Index"
          value={dataStore.getGloData(mapType)["I"]}
          valueStyle={{ fontSize: "20px" }}
          precision={3}
        />
      </Col>
      <Col span={6}>
        <Statistic
          title="Expected Index"
          value={dataStore.getGloData(mapType)["Expected I"]}
          valueStyle={{ fontSize: "20px" }}
          precision={3}
        />
      </Col>
      <Col span={6}>
        <Statistic
          title="P-value"
          value={dataStore.getGloData(mapType)["p-value"]}
          valueStyle={{ fontSize: "20px" }}
          precision={3}
        />
      </Col>
    </Row>
  );
});

export default Global;
