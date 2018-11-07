import React from 'react';
import { Button,Label,
  Input, Col, Nav, NavItem, NavLink, Row
   } from 'reactstrap';
import classnames from 'classnames';  
import SkyLight from 'react-skylight';

class Showimage extends React.Component {
  constructor(props){
    super(props);
    this.initial_method = this.initial_method.bind(this)
    this.state = {};    
  }

  componentDidMount() {
    this.props.onRef(this)
  }
  componentWillUnmount() {
    this.props.onRef(undefined)    
  }

  initial_method(name,image) { 
      this.setState({title:name,
          image:image
      })
    this.simpleDialog.show() 
  }


  render() {
    var myBigGreenDialog = {
        width: '50%',
        minHeight: '3px',      
      };
      var image={
        width: '50%',
        minHeight: '3px',
      };
    return (
      <div>

        <SkyLight  dialogStyles={myBigGreenDialog}  hideOnOverlayClicked ref={ref => this.simpleDialog = ref} title={this.state.title}>
        <hr />
          <Row style={{ display: 'flex', justifyContent: 'center'}}>{this.state.subtitle}</Row><br />
              <Row style={{ display: 'flex', justifyContent: 'center'}}>   
              <img style={{'height':'300px', 'width':'95%'}} src={'data:image/jpeg;base64, ' + this.state.image} alt="Red dot"></img> 
              </Row> <br/> 
              <Row>
                    <Button color="tn-color" style={{marginLeft:'38%'}} onClick={() => this.simpleDialog.hide()}  className="btn btn-yellow">Close</Button> 
              </Row>
        </SkyLight>

       
      
      </div>
    )
  }
}

export default Showimage;