/*
 * @author: Hanchen Cai <hanchenc@student.unimelb.edu.au>
 */

import {
  Form,
  Card,
  Radio,
  Space,
  Select,
  InputNumber,
  Input,
  Spin,
  Button,
} from "antd";
import React from "react";
import { useStore } from "../stores";
import { action } from "mobx";
import { observer } from "mobx-react-lite";
import { SyncOutlined } from "@ant-design/icons";

const MapForm = observer(({ formType, updateMap }) => {
  const { dataStore } = useStore();
  const fetchData = dataStore.getFetchData(formType);
  // const setDataLoaded = dataStore.getSetDataLoaded(props.formType);
  // const isDataLoaded = dataStore.getIsDataLoaded(props.formType);

  // const onFinish;

  const getMapForm = (formType) => {
    if (formType === "avgToxMap") {
      return null;
    } else if (formType === "locToxMap") {
      return (
        <>
          <Form.Item label="Rule" style={{ marginBottom: 0 }}>
            <Radio.Group
              onChange={(e) => dataStore.setLocToxRule(e.target.value)}
              value={dataStore.locToxRule}
              buttonStyle="solid"
            >
              <Radio.Button value="rook">Rook</Radio.Button>
              <Radio.Button value="queen">Queen</Radio.Button>
            </Radio.Group>
          </Form.Item>
          <Form.Item label="Alpha" style={{ marginBottom: 0 }}>
            <InputNumber
              step={0.01}
              value={dataStore.locToxAlpha}
              onChange={dataStore.setLocToxAlpha}
              style={{ width: "70px" }}
            />
          </Form.Item>
        </>
      );
    } else if (formType === "avgSentMap") {
      return (
        <>
          <Form.Item label="Label" style={{ marginBottom: 0 }}>
            <Select
              value={dataStore.avgSentLabel}
              onChange={(e) => dataStore.setAvgSentLabel(e)}
              options={[
                { value: "positive", label: "Positive" },
                { value: "neutral", label: "Neutral" },
                { value: "negative", label: "Negative" },
              ]}
            />
          </Form.Item>
        </>
      );
    } else if (formType === "locSentMap") {
      return (
        <>
          <Form.Item label="Rule" style={{ marginBottom: 0 }}>
            <Radio.Group
              onChange={(e) => dataStore.setLocSentRule(e.target.value)}
              value={dataStore.locSentRule}
              buttonStyle="solid"
            >
              <Radio.Button value="rook">Rook</Radio.Button>
              <Radio.Button value="queen">Queen</Radio.Button>
            </Radio.Group>
          </Form.Item>
          <Form.Item label="Label" style={{ marginBottom: 0 }}>
            <Select
              value={dataStore.locSentLabel}
              onChange={(e) => dataStore.setLocSentLabel(e)}
              options={[
                { value: "positive", label: "Positive" },
                { value: "neutral", label: "Neutral" },
                { value: "negative", label: "Negative" },
              ]}
              style={{ width: "100px" }}
            />
          </Form.Item>
          <Form.Item label="Alpha" style={{ marginBottom: 0 }}>
            <InputNumber
              step={0.01}
              value={dataStore.locSentAlpha}
              onChange={dataStore.setLocSentAlpha}
              style={{ width: "70px" }}
            />
          </Form.Item>
        </>
      );
    } else if (formType === "statMap") {
      return (
        <>
          <Form.Item label="Type" style={{ marginBottom: 0 }}>
            <Radio.Group
              onChange={(e) => dataStore.setStatType(e.target.value)}
              value={dataStore.statType}
              buttonStyle="solid"
            >
              <Radio.Button value="crime">Crime</Radio.Button>
              <Radio.Button value="rent">Rent</Radio.Button>
            </Radio.Group>
          </Form.Item>
        </>
      );
    }
  };

  const getMoranTypeSelect = (formType) => {
    if (formType === "locToxMap") {
      return (
        <Form.Item label="Data" style={{ marginBottom: 0 }}>
          <Select
            value={dataStore.locToxType}
            onChange={(e) => {
              dataStore.setLocToxType(e);
              dataStore.updateLocToxDataByType();
              updateMap();
            }}
            options={[
              { value: "LISA", label: "Local Moran's Index" },
              { value: "EI", label: "Index Expectation" },
              { value: "VI", label: "Index Variance" },
              { value: "ZI", label: "Standardized Index" },
              { value: "p_value", label: "P_value" },
              { value: "is_significant", label: "is significant" },
            ]}
            style={{ width: "170px" }}
          />
        </Form.Item>
      );
    } else if (formType === "locSentMap") {
      return (
        <Form.Item label="Data" style={{ marginBottom: 0 }}>
          <Select
            value={dataStore.locSentType}
            onChange={(e) => {
              dataStore.setLocSentType(e);
              dataStore.updateLocSentDataByType();
              updateMap();
            }}
            options={[
              { value: "LISA", label: "Local Moran's Index" },
              { value: "EI", label: "Index Expectation" },
              { value: "VI", label: "Index Variance" },
              { value: "ZI", label: "Standardized Index" },
              { value: "p_value", label: "P_value" },
              { value: "is_significant", label: "is significant" },
            ]}
            style={{ width: "170px" }}
          />
        </Form.Item>
      );
    }
  };

  return (
    <Form>
      <Space size={10} align="baseline">
        {getMapForm(formType)}
        {getMoranTypeSelect(formType)}
        <Form.Item>
          <Button
            type="primary"
            loading={!dataStore.isDataLoaded(formType)}
            icon={<SyncOutlined />}
            onClick={action((e) => {
              dataStore.setDataLoaded(formType, false);
              fetchData().then(() => {
                updateMap();
                dataStore.setDataLoaded(formType, true);
              });
              if (formType === "locToxMap") {
                dataStore.fetchGloToxData();
              } else if (formType === "locSentMap") {
                dataStore.fetchGloSentData();
              }
              e.stopPropagation();
            })}
          />
        </Form.Item>
      </Space>
    </Form>
  );
});

export default MapForm;
