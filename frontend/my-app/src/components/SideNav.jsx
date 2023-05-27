/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

// import React from "react";
import { useState } from "react";
import {
  FireOutlined,
  SmileOutlined,
  AppstoreOutlined,
  DotChartOutlined,
} from "@ant-design/icons";
import { Link } from "react-router-dom";
import { Layout, Menu } from "antd";
import { useLocation } from "react-router";
import React from "react";
const { Sider } = Layout;

function SideNav() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const selectedKey = location.pathname;

  function getItem(key, label, icon, children) {
    return {
      key,
      icon,
      children,
      label,
    };
  }

  const items = [
    getItem(
      "/",
      <Link to="/">Toxicity</Link>,
      <FireOutlined style={{ fontSize: "18px" }} />
    ),
    getItem(
      "/sentiment",
      <Link to="/sentiment">Sentiment</Link>,
      <SmileOutlined style={{ fontSize: "18px" }} />
    ),
    getItem(
      "/statistic",
      <Link to="/statistic">Statistic</Link>,
      <DotChartOutlined style={{ fontSize: "18px" }} />
    ),
  ];

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={(value, type) => {
        setCollapsed(value);
        window.dispatchEvent(new Event("resize"));
        const logo = document.getElementById("web-logo");
        if (logo.innerHTML === "Team 80") {
          logo.innerHTML = "80";
        } else {
          setTimeout(() => {
            logo.innerHTML = "Team 80";
          }, 200);
        }
      }}
    >
      <div
        id="web-logo"
        style={{
          height: 32,
          margin: 16,
          textAlign: "center",
          fontSize: "22px",
          color: "white",
          fontFamily: "lilitaone",
        }}
      >
        Team 80
      </div>
      <Menu
        theme="dark"
        selectedKeys={selectedKey}
        mode="inline"
        items={items}
      />
    </Sider>
  );
}

export default SideNav;
