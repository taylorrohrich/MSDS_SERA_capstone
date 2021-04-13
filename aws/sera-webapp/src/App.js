import logo from './logo.svg';
import {BrowserRouter as Router, Route, Switch } from "react-router-dom";
import {Tracker,Query} from "./pages"
import {Nav} from "./components"
import './App.css';

const App = ()=>{
  return <Router>
    <Nav/>
    <Switch>
      <Route path="/query">
        <Query/>
      </Route>
      <Route path ="/">
        <Tracker/>
      </Route>
    </Switch>
  </Router>
}
export default App;
