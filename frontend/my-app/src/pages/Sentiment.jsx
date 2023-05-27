/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

import React from "react";
import Map from "@/components/Map";
import { Row, Col } from "antd";
import Global from "@/components/Global";
import Chart from "@/components/Chart";

const Sentiment = () => {
  return (
    // <Layout className="site-layout">
    //   <Content
    //     style={{
    //       margin: "16px 16px 0 16px",
    //     }}
    //   >
    <Row gutter={[24, 24]}>
      <Col span={12}>
        <Map mapTitle="Average Sentiment" mapType="avgSentMap" />
      </Col>
      <Col span={12}>
        <Map mapTitle="Autocorrelation Sentiment" mapType="locSentMap" />
      </Col>
      <Col span={12}>
        <Chart
          chartTitle="Twitter Sentiment Distribution"
          chartType="twSentDistPie"
        />
      </Col>
      <Col span={12}>
        <Chart
          chartTitle="Mastodon Sentiment Distribution"
          chartType="mdSentDistPie"
        />
      </Col>
      <Col span={12}>
        <Chart chartTitle="Twitter Top Word Count" chartType="twWordCntBar" />
      </Col>
      <Col span={12}>
        <Chart chartTitle="Mastodon Top Word Count" chartType="mdWordCntBar" />
      </Col>
    </Row>
  );
};

export default Sentiment;
