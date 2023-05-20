import { Card, Layout, theme } from "antd";
const { Header, Sider, Content } = Layout;

import Charts from "./components/Charts";
import Map from "./components/Map";
import SideNav from "./components/SideNav";
import React from "react";

const App = () => {
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  return (
    <Layout
      style={{
        minHeight: "100vh",
      }}
    >
      <SideNav />
      <Layout className="site-layout">
        <Header
          style={{
            padding: 0,
            background: colorBgContainer,
          }}
        />
        <Content
          style={{
            margin: "16px 16px 0 16px",
          }}
        >
          <Card>Filters</Card>
          <Map />
        </Content>
      </Layout>
    </Layout>
  );
};

export default App;
