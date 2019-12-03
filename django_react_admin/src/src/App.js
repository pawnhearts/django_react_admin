import React, { Component } from "react";
import { Admin, Resource, ListGuesser, EditGuesser, ShowGuesser } from 'react-admin';
import drfProvider from 'ra-data-drf';
const apiUrl = "api";
const dataProvider =
  drfProvider(apiUrl);

class App extends Component {
  render() {
    let res = this.state.resources.map((i) => {return <Resource name={i} list={ListGuesser} edit={EditGuesser} show={ShowGuesser} />;});

    return (
      <Admin dataProvider={dataProvider}>
        {res}
      </Admin>
    );
  }
  componentDidMount() {
    fetch(apiUrl+'/').then(response => response.json()).then(response => {
          let res = response.reduce((a, cur) => {
            let b=cur.models.map((m) => {return m.admin_url.replace(/\/$/, "");});
            return [...a, ...b];
            }
            ,[]);
            this.setState({'resources': res});
        }
    );
    document.title = "Django Admin";
  }
  constructor(props) {
    super(props);
    this.state = {
      resources: []
    };
  }

}

export default App;

