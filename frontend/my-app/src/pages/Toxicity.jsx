/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

import Map from "@/components/Map";
import Chart from "@/components/Chart";
import { Row, Col } from "antd";
import { observer } from "mobx-react-lite";

const Toxicity = () => {
  return (
    <Row gutter={[24, 24]}>
      <Col span={12}>
        <Map mapTitle="Average Toxicity" mapType="avgToxMap" />
      </Col>
      <Col span={12}>
        <Map mapTitle="Autocorrelation Toxicity" mapType="locToxMap" />
      </Col>
      <Col span={12}>
        <Chart chartTitle="Toxicity vs #Followers" chartType="fllrScatter" />
      </Col>
      <Col span={12}>
        <Chart chartTitle="Toxicity vs #Following" chartType="fllgScatter" />
      </Col>
      {/*   */}
      {/* <Col span={12}>
    <Map mapTitle="Local Autocorrelation Sentiment" formType="locSent" />
  </Col>
  <Col span={12}>
    <Map
      mapTitle="Significant Local Autocorrelation Sentiment"
      formType="sigSent"
    />
  </Col> */}
    </Row>
  );
};

export default Toxicity;
