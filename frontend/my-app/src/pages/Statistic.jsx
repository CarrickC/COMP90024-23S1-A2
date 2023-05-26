import React from "react";
import { Row, Col } from "antd";
import Map from "@/components/Map";
import Chart from "@/components/Chart";

const Statistic = () => {
  return (
    <Row gutter={[24, 24]}>
      <Col span={24}>
        <Map mapTitle="Suburb Statistic Map" mapType="statMap" />
      </Col>
      <Col span={8}>
        <Chart chartTitle="Jobs" chartType="jobBar" />
      </Col>
      <Col span={8}>
        <Chart chartTitle="Patrons" chartType="patronBar" />
      </Col>
      <Col span={8}>
        <Chart chartTitle="Parking Slots" chartType="pkSpcBar" />
      </Col>
      <Col span={24}>
        <Chart chartTitle="Population by Gender" chartType="popByGenderBar" />
      </Col>
      <Col span={24}>
        <Chart chartTitle="Population by Age" chartType="popByAgeBar" />
      </Col>
    </Row>
  );
};

export default Statistic;
