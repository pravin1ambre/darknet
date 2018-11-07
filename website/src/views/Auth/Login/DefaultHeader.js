import React, { Component } from 'react';
import { Badge, DropdownItem, DropdownMenu, FormGroup, Input, DropdownToggle, Nav, NavItem, NavLink, Label } from 'reactstrap';
import PropTypes from 'prop-types';

import { AppHeaderDropdown, AppNavbarBrand, AppSidebarToggler } from '@coreui/react';
import logo from '../../../assets/img/brand/logo.jpg'
import sygnet from '../../../assets/img/brand/logo.jpg'
// import cookie from 'react-cookies';
// import Label from '../../../../../../../.cache/typescript/2.6/node_modules/@types/reactstrap/lib/Label';

const propTypes = {
  children: PropTypes.node,
};

const defaultProps = {};

class DefaultHeader extends Component {

  constructor(props) {
    super(props);
  }

  render() {

    // eslint-disable-next-line
    const { children, ...attributes } = this.props;

    return (
      <React.Fragment >
        <AppNavbarBrand 
          full={{src: logo,  width: 160, height: '50'}}
          minimized={{ src: sygnet, width: 30, height: 30, alt: 'logo' }}
        />       
      </React.Fragment>
    );
  }
}

DefaultHeader.propTypes = propTypes;
DefaultHeader.defaultProps = defaultProps;

export default DefaultHeader;
