import React from 'react';
import { Menu } from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css'; // Import Semantic UI CSS
import './App.css';
import PredictForm from './PredictForm';

function App() {
  return (
    <div className="App">
      <Menu inverted className="menu">
        <Menu.Item name='home' />
      </Menu>
      <PredictForm />
    </div>
  );
}

export default App;
