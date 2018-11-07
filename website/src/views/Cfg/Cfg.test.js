import React from 'react';
import ReactDOM from 'react-dom';
import Cfg from './Cfg';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<Cfg />, div);
  ReactDOM.unmountComponentAtNode(div);
});
