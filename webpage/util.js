class MyList extends React.Component {
  constructor(...args) {
    super(...args);
    this.state = {
      loading: true,
      error: null,
      data: null
    };
  }

  componentDidMount() {
    const url = 'http://localhost:2345/cities/Des%20Moines';
    $.getJSON(url)
     .done(
      (value) => this.setState({
        loading: false,
        data: value
      })
    ).fail(
      (jqXHR, textStatus) => this.setState({
        loading: false,
        error: jqXHR.status
      })
    );
  }

  render() {
    if (this.state.loading) {
      return <span>Loading...</span>;
    } else if (this.state.error !== null) {
      return <span>Error: {this.state.error}</span>;
    } else {
      console.log(this.state.data.data);
      const dataDict = this.state.data.data;
      let results = [];
      Object.keys(dataDict).map((key, index) => {
        if (key === "alternate_names") {
          let altNameList = [];
          let cnt = 1;
          dataDict[key].forEach(function(element) {
            if (cnt == 1) {
              altNameList.push(<tr key={key+cnt}><td>{key}</td><td>{element}</td></tr>);
            } else {
              altNameList.push(<tr key={key+cnt}><td></td><td>{element}</td></tr>);
            }
            cnt++;
          });
          results.push(altNameList);
        } else {
          let item = <tr key={key}><td>{key}</td><td>{dataDict[key]}</td></tr>;
          results.push(item);
        }
      })
      return (
          <div>
            <table><tbody>{results}</tbody></table>
          </div>
      );
    }
  }
};

ReactDOM.render(
  <MyList/>,
  document.getElementById('example')
);
