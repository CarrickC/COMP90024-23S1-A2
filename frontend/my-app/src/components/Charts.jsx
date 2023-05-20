// import React from "react";
import { Card, Col } from "antd";
import ReactECharts from "echarts-for-react";
import { useEffect, useState } from "react";
import axios from "axios";
import Map from "./Map";
import React from "react";

function Charts() {
  const [data, setData] = useState({ 0: 0 });

  useEffect(() => {
    async function getData() {
      const res = await axios.get("http://127.0.0.1:8080/api_2");
      // console.log(res.data);
      // console.log(res.data);
      setData(res.data.data);
      console.log(data);
    }

    getData();
  }, []);

  return (
    <Col>
      <Card
        style={{
          margin: "16px",
        }}
      >
        <ReactECharts
          style={{ minHeight: 500 }}
          option={{
            xAxis: {
              type: "category",
              data: Object.keys(data),
            },
            yAxis: {
              type: "value",
            },
            series: [
              {
                data: Object.values(data),
                type: "bar",
              },
            ],
          }}
        />
      </Card>
      <Card>
        <Map />
      </Card>
    </Col>
  );
}

export default Charts;
