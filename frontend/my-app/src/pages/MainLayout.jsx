import { Card, Col, Layout, Row, Space, Spin, theme } from "antd";
const { Header, Sider, Content } = Layout;

import Map from "@/components/Map";
import SideNav from "@/components/SideNav";
import React from "react";
import { Outlet } from "react-router";

const MainLayout = () => {
  return (
    <Layout
      style={{
        minHeight: "100vh",
      }}
    >
      <SideNav />
      <Layout>
        <Content
          style={{
            margin: "24px 50px 24px 24px",
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
