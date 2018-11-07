import React from 'react';
import Loadable from 'react-loadable'


function Loading() {
  return <div>Loading...</div>;
}


const Image = Loadable({
  loader: () => import('./views/Image/Image'),
  loading: Loading,
});



const Cfg = Loadable({
  loader: () => import('./views/Cfg'),
  loading: Loading,
});

// https://github.com/ReactTraining/react-router/tree/master/packages/react-router-config
const routes = [ 
  { path: '/configuration', name: 'Configuration', component: Cfg },
  { path: '/image', name: 'Image', component: Image },
];

export default routes;
