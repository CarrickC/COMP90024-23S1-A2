// @ts-nocheck
import {
  makeAutoObservable,
  makeObservable,
  observable,
  action,
  runInAction,
  computed,
  toJS,
} from "mobx";
import * as echarts from "echarts";
import _ from "lodash";

class DataStore {
  // url = "http://127.0.0.1:8080";
  url = "http://172.26.133.136:8080";

  isLoading = false;

  isMapLoaded = false;

  // isDataLoaded = false;

  melbMap = null;

  rule = "rook";

  // Toxicity
  locToxRule = "rook";
  locToxAlpha = 0.05;
  locToxType = "p_value";

  // Sentiment
  avgSentLabel = "positive";

  locSentRule = "rook";
  locSentLabel = "positive";
  locSentType = "p_value";
  locSentAlpha = 0.05;

  // Stat
  statType = "crime";

  // Word count
  wordCntSuburb = "all";

  // Data
  avgToxData = [];
  isAvgToxDataLoaded = false;

  locToxData = [];
  isLocToxDataLoaded = false;

  avgSentData = [];
  isAvgSentDataLoaded = false;

  locSentData = [];
  isLocSentDataLoaded = false;

  statData = [];
  isStatDataLoaded = false;

  twWordCntData = [];
  isTWWordCntDataLoaded = false;

  mdWordCntData = [];
  isMDWordCntDataLoaded = false;

  twSentDistData = [];
  isTWSentDistDataLoaded = false;

  mdSentDistData = [];
  isMDSentDistDataLoaded = false;

  popByAgeData = [];
  isPopByAgeDataLoaded = false;

  popByGenderData = [];
  isPopByGenderDataLoaded = false;

  pkSpcByTypeData = [];
  isPkSpcByTypeDataLoaded = false;

  patronData = [];
  isPatronDataLoaded = false;

  jobData = [];
  isJobDataLoaded = false;

  fllrData = { data: [], avgs: [] };
  isFllrDataLoaded = false;

  fllgData = { data: [], avgs: [] };
  isFllgDataLoaded = false;

  gloToxData = {
    I: 0,
    "Expected I": 0,
    "p-value": 0,
  };
  gloSentData = {
    I: 0,
    "Expected I": 0,
    "p-value": 0,
  };

  constructor() {
    // makeObservable(this, {
    //   isLoading: observable,
    //   setLoading: action,
    // });
    makeAutoObservable(this);
  }

  setDataLoaded = (type, isLoaded) => {
    if (type === "avgSentMap") {
      this.isAvgSentDataLoaded = isLoaded;
    } else if (type === "locSentMap") {
      this.isLocSentDataLoaded = isLoaded;
    } else if (type === "sigSentMap") {
      this.isSigSentDataLoaded = isLoaded;
    } else if (type === "avgToxMap") {
      this.isAvgToxDataLoaded = isLoaded;
    } else if (type === "locToxMap") {
      this.isLocToxDataLoaded = isLoaded;
    } else if (type === "sigToxMap") {
      this.isSigToxDataLoaded = isLoaded;
    } else if (type === "statMap") {
      this.isStatDataLoaded = isLoaded;
    } else if (type === "twWordCntBar") {
      this.isTWWordCntDataLoaded = isLoaded;
    } else if (type === "mdWordCntBar") {
      this.isMDWordCntDataLoaded = isLoaded;
    } else if (type === "twSentDistPie") {
      this.isTWSentDistDataLoaded = isLoaded;
    } else if (type === "mdSentDistPie") {
      this.isMDSentDistDataLoaded = isLoaded;
    } else if (type === "fllrScatter") {
      this.isFllrDataLoaded = isLoaded;
    } else if (type === "fllgScatter") {
      this.isFllgDataLoaded = isLoaded;
    } else if (type === "popByAgeBar") {
      this.isPopByAgeDataLoaded = isLoaded;
    } else if (type === "popByGenderBar") {
      this.isPopByGenderDataLoaded = isLoaded;
    } else if (type === "pkSpcBar") {
      this.isPkSpcByTypeDataLoaded = isLoaded;
    } else if (type === "patronBar") {
      this.isPatronDataLoaded = isLoaded;
    } else if (type === "jobBar") {
      this.isJobDataLoaded = isLoaded;
    }
  };

  isDataLoaded = (type) => {
    if (type === "avgSentMap") {
      return this.isAvgSentDataLoaded;
    } else if (type === "locSentMap") {
      return this.isLocSentDataLoaded;
    } else if (type === "avgToxMap") {
      return this.isAvgToxDataLoaded;
    } else if (type === "locToxMap") {
      return this.isLocToxDataLoaded;
    } else if (type === "statMap") {
      return this.isStatDataLoaded;
    } else if (type === "twWordCntBar") {
      return this.isTWWordCntDataLoaded;
    } else if (type === "mdWordCntBar") {
      return this.isMDWordCntDataLoaded;
    } else if (type === "twSentDistPie") {
      return this.isTWSentDistDataLoaded;
    } else if (type === "mdSentDistPie") {
      return this.isMDSentDistDataLoaded;
    } else if (type === "fllrScatter") {
      return this.isFllrDataLoaded;
    } else if (type === "fllgScatter") {
      return this.isFllgDataLoaded;
    } else if (type === "popByAgeBar") {
      return this.isPopByAgeDataLoaded;
    } else if (type === "popByGenderBar") {
      return this.isPopByGenderDataLoaded;
    } else if (type === "pkSpcBar") {
      return this.isPkSpcByTypeDataLoaded;
    } else if (type === "patronBar") {
      return this.isPatronDataLoaded;
    } else if (type === "jobBar") {
      return this.isJobDataLoaded;
    }
  };

  setMapLoaded = (isLoaded) => {
    this.isMapLoaded = isLoaded;
  };

  setLocToxRule = (rule) => {
    this.locToxRule = rule;
  };

  setLocToxAlpha = (alpha) => {
    this.locToxAlpha = alpha;
  };

  setLocToxType = (type) => {
    this.locToxType = type;
  };

  setAvgSentLabel = (label) => {
    this.avgSentLabel = label;
  };

  setLocSentRule = (rule) => {
    this.locSentRule = rule;
  };

  setLocSentLabel = (label) => {
    this.locSentLabel = label;
  };

  setLocSentAlpha = (alpha) => {
    this.locSentAlpha = alpha;
  };

  setLocSentType = (type) => {
    this.locSentType = type;
  };

  setStatType = (type) => {
    this.statType = type;
  };

  setWordCntSuburb = (suburb) => {
    this.wordCntSuburb = suburb;
  };

  fetchMap = async () => {
    const res = await fetch(`${this.url}/geojson`);
    const geojson = await res.json();

    geojson.features.map(
      (item) => (item.properties.name = item.properties.SA2_NAME21)
    );

    runInAction(() => {
      this.melbMap = geojson;
    });
  };

  fetchGloToxData = async () => {
    const res = await fetch(`${this.url}/global_autocorrelation`);
    const data = await res.json();
    runInAction(() => {
      this.gloToxData = data;
    });
  };

  fetchGloSentData = async () => {
    const res = await fetch(
      `${this.url}//global_autocorrelation_sentiment/${this.locSentLabel}`
    );
    const data = await res.json();

    runInAction(() => {
      this.gloSentData = data;
    });
  };

  fetchAvgToxData = async () => {
    const res = await fetch(`${this.url}/average_toxicity`);
    const data = await res.json();

    runInAction(() => {
      this.avgToxData = Object.entries(data.data).map(([key, value]) => ({
        name: key,
        value: value.average_toxicity,
      }));
    });
  };

  fetchLocToxData = async () => {
    const res = await fetch(
      `${this.url}/local_autocorrelation?rule=${this.locToxRule}&alpha=${this.locToxAlpha}`
    );
    const data = await res.json();

    runInAction(() => {
      this.locToxData = Object.entries(data.data).map(([key, value]) => ({
        name: key,
        value: value.p_value,
        ...value,
      }));
      this.locToxType = "p_value";
    });
  };

  fetchAvgSentData = async () => {
    const res = await fetch(`${this.url}/average_sent/${this.avgSentLabel}`);
    const data = await res.json();

    runInAction(() => {
      this.avgSentData = data.map((item) => ({
        name: item.suburb,
        value: item.value.average,
        ...item.value,
      }));
    });
  };

  fetchLocSentData = async () => {
    const res = await fetch(
      `${this.url}/local_autocorrelation_sentiment/${this.locSentLabel}?rule=${this.locSentRule}&alpha=${this.locSentAlpha}`
    );
    const data = await res.json();
    runInAction(() => {
      this.locSentData = Object.entries(data.data).map(([key, value]) => ({
        name: key,
        value: value.p_value,
        ...value,
      }));
      this.locSentType = "p_value";
    });
  };

  fetchStatData = async () => {
    if (this.statType === "crime") {
      const res = await fetch(`${this.url}/crime_data`);
      const data = await res.json();

      runInAction(() => {
        this.statData = Object.entries(data.crime_data).map(([_, value]) => ({
          name: value["Suburb/Town Name"],
          value: value["Offence Count"],
        }));
      });
    } else if (this.statType === "rent") {
      const res = await fetch(`${this.url}/rent_data`);
      const data = await res.json();

      runInAction(() => {
        this.statData = Object.entries(data.rent_data).map(([_, value]) => ({
          name: value["SA2_NAME21"],
          value: value["average_rent"],
        }));
      });
    }
  };

  fetchTWWordCntData = async () => {
    let URL = "";
    if (this.wordCntSuburb === "all") {
      URL = `${this.url}/top_word_counts?start_date=2018-02-10T00:00:00.000Z&end_date=2023-02-10T23:59:59.999Z`;
    } else {
      URL = `${this.url}/top_word_counts?start_date=2018-02-10T00:00:00.000Z&end_date=2023-02-10T23:59:59.999Z&suburb=${this.wordCntSuburb}`;
    }

    const res = await fetch(URL);
    const data = await res.json();

    runInAction(() => {
      this.twWordCntData = Object.entries(data.data)
        .map(([key, value]) => ({
          name: key,
          value: value,
        }))
        .filter(({ _, value }) => value > 200)
        .sort((a, b) => b.value - a.value);
    });
  };

  fetchMDWordCntData = async () => {
    let URL = "";
    if (this.wordCntSuburb === "all") {
      URL = `${this.url}/top_word_counts_mastodon`;
    } else {
      URL = `${this.url}/top_word_counts_mastodon`;
    }

    const res = await fetch(URL);
    const data = await res.json();

    runInAction(() => {
      this.mdWordCntData = Object.entries(data.data)
        .map(([key, value]) => ({
          name: key,
          value: value,
        }))
        .sort((a, b) => b.value - a.value);
    });
  };

  fetchPopByGenderData = async () => {
    const res = await fetch(`${this.url}/total_value_by_gender`);
    const data = await res.json();

    runInAction(() => {
      this.popByGenderData = Object.entries(data.data).map(([key, value]) => ({
        Suburb: key,
        ...value,
      }));
    });
  };

  fetchPopByAgeData = async () => {
    const res = await fetch(`${this.url}/total_value_by_age`);
    const data = await res.json();

    runInAction(() => {
      this.popByAgeData = Object.entries(data.data).map(([key, value]) => ({
        Suburb: key,
        "Age 0-19":
          value["Age 0-4"] +
          value["Age 5-9"] +
          value["Age 10-14"] +
          value["Age 15-19"],
        "Age 20-39":
          value["Age 20-24"] +
          value["Age 25-29"] +
          value["Age 30-34"] +
          value["Age 35-39"],
        "Age 40-59":
          value["Age 40-44"] +
          value["Age 45-49"] +
          value["Age 50-54"] +
          value["Age 55-59"],
        "Age 60+":
          value["Age 60-64"] +
          value["Age 65-69"] +
          value["Age 70-74"] +
          value["Age 75-79"] +
          value["Age 80-84"] +
          value["Age 85+"],
      }));
    });
  };

  fetchPkSpcByTypeData = async () => {
    const res = await fetch(`${this.url}/total_spaces_by_area_and_type`);
    const data = await res.json();

    runInAction(() => {
      this.pkSpcByTypeData = Object.entries(data.data)
        .map(([key, value]) => ({
          Suburb: key,
          ...value,
        }))
        .sort((a, b) => b.Commercial - a.Commercial);
    });
  };

  fetchJobData = async () => {
    const res = await fetch(`${this.url}/total_value_by_jobsforecasts`);
    const data = await res.json();

    runInAction(() => {
      this.jobData = Object.entries(data.data)
        .map(([key, value]) => ({
          Suburb: key,
          Jobs: value,
        }))
        .sort((a, b) => b.Jobs - a.Jobs);
    });
  };

  fetchPatronData = async () => {
    const res = await fetch(`${this.url}/total_patrons_by_area`);
    const data = await res.json();

    runInAction(() => {
      this.patronData = Object.entries(data.data)
        .map(([key, value]) => ({
          Suburb: key,
          Patrons: value,
        }))
        .sort((a, b) => b.Patrons - a.Patrons);
    });
  };

  fetchTWSentDistData = async () => {
    const res = await fetch(`${this.url}/sentiment_distribution?db=twitter`);
    const data = await res.json();

    runInAction(() => {
      this.twSentDistData = Object.entries(data.data).map(([key, value]) => ({
        name: key,
        value: value,
      }));
    });
  };

  fetchMDSentDistData = async () => {
    const res = await fetch(`${this.url}/sentiment_distribution?db=mastodon`);
    const data = await res.json();

    runInAction(() => {
      this.mdSentDistData = Object.entries(data.data).map(([key, value]) => ({
        name: key,
        value: value,
      }));
    });
  };

  fetchFllrData = async () => {
    const res = await fetch(`${this.url}/followers_scatter`);
    const data = await res.json();

    runInAction(() => {
      const temp = data.data.followers_count
        .map((value, index) => [value, data.data.toxicity[index]])
        .filter(([value, _]) => value < 2000);

      this.fllrData.data = temp;
      this.fllrData.avgs = this.getAvgLine(temp);
    });
  };

  fetchFllgData = async () => {
    const res = await fetch(`${this.url}/following_scatter`);
    const data = await res.json();

    runInAction(() => {
      const temp = data.data.following_count
        .map((value, index) => [value, data.data.toxicity[index]])
        .filter(([value, _]) => value < 2000);

      this.fllgData.data = temp;
      this.fllgData.avgs = this.getAvgLine(temp);
    });
  };

  getGloData = (type) => {
    if (type === "locToxMap") {
      return this.gloToxData;
    } else if (type === "locSentMap") {
      return this.gloSentData;
    }
  };

  getFetchData = (type) => {
    if (type === "avgToxMap") {
      return this.fetchAvgToxData;
    } else if (type === "locToxMap") {
      return this.fetchLocToxData;
    } else if (type === "avgSentMap") {
      return this.fetchAvgSentData;
    } else if (type === "locSentMap") {
      return this.fetchLocSentData;
    } else if (type === "statMap") {
      return this.fetchStatData;
    } else if (type === "twWordCntBar") {
      return this.fetchTWWordCntData;
    } else if (type === "mdWordCntBar") {
      return this.fetchMDWordCntData;
    } else if (type === "twSentDistPie") {
      return this.fetchTWSentDistData;
    } else if (type === "mdSentDistPie") {
      return this.fetchMDSentDistData;
    } else if (type === "fllrScatter") {
      return this.fetchFllrData;
    } else if (type === "fllgScatter") {
      return this.fetchFllgData;
    } else if (type === "popByAgeBar") {
      return this.fetchPopByAgeData;
    } else if (type === "popByGenderBar") {
      return this.fetchPopByGenderData;
    } else if (type === "pkSpcBar") {
      return this.fetchPkSpcByTypeData;
    } else if (type === "patronBar") {
      return this.fetchPatronData;
    } else if (type === "jobBar") {
      return this.fetchJobData;
    }
  };

  getData = (type) => {
    if (type === "avgToxMap") {
      return this.avgToxData;
    } else if (type === "locToxMap") {
      return this.locToxData;
    } else if (type === "avgSentMap") {
      return this.avgSentData;
    } else if (type === "locSentMap") {
      return this.locSentData;
    } else if (type === "statMap") {
      return this.statData;
    } else if (type === "twWordCntBar") {
      return this.twWordCntData;
    } else if (type === "mdWordCntBar") {
      return this.mdWordCntData;
    } else if (type === "twSentDistPie") {
      return this.twSentDistData;
    } else if (type === "mdSentDistPie") {
      return this.mdSentDistData;
    } else if (type === "fllrScatter") {
      return this.fllrData;
    } else if (type === "fllgScatter") {
      return this.fllgData;
    } else if (type === "popByAgeBar") {
      return this.popByAgeData;
    } else if (type === "popByGenderBar") {
      return this.popByGenderData;
    } else if (type === "pkSpcBar") {
      return this.pkSpcByTypeData;
    } else if (type === "patronBar") {
      return this.patronData;
    } else if (type === "jobBar") {
      return this.jobData;
    }
  };

  updateLocToxDataByType = () => {
    this.locToxData.map((item) => {
      item.value = item[this.locToxType];
      return item;
    });
  };

  updateLocSentDataByType = () => {
    this.locSentData.map((item) => {
      item.value = item[this.locSentType];
      return item;
    });
  };

  getAvgLine = (data) => {
    const xs = _.range(100, 2100, 100);
    const avgs = [];

    for (let i = 0; i < xs.length; i++) {
      let total = 0;
      let count = 0;

      for (let j = 0; j < data.length; j++) {
        if (data[j][0] >= xs[i] - 100 && data[j][0] < xs[i]) {
          total += data[j][1];
          count += 1;
        }
      }

      if (count > 0) {
        avgs.push([xs[i], total / count]);
      }
    }
    return avgs;
  };
}

export default DataStore;
