import React from 'react';
import { Button,Label,
  Input, FormGroup, Row, Col
   } from 'reactstrap';
import SkyLight from 'react-skylight';
import axios from 'axios';
import Env from '../../enviorment';

class Action extends React.Component {
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

  initial_method(actions) { 
    console.log(actions)
      this.setState({title:actions.mac_address,
        object_sync : false,
        source_sync:actions.source_sync,
        object_sync:actions.object_sync,
        thumbnail_sync:actions.thumbnail_sync
      })
    this.simpleDialog.show() 
  }

  save(){
    this.simpleDialog.hide()
    axios.get(Env.Url+'detect-object/'+this.state.title).then(res =>{
      // this.simpleDialog.hide()
    })
  }
  objects(){
    this.setState({object_sync : !this.state.object_sync})
  }


  render() {
    var myBigGreenDialog = {
        width: '30%',
        minHeight: '3px',
        left : '80%'      
      };
    return (
      <div>

        <SkyLight  dialogStyles={myBigGreenDialog}  hideOnOverlayClicked ref={ref => this.simpleDialog = ref}>
        <div row><h6>{this.state.title}</h6></div>
        <hr />
          <Row style={{ display: 'flex', justifyContent: 'center'}}>{this.state.subtitle}</Row><br />
             
              <Row>
                <Col xs="12" sm="6">
                <Label>source_sync</Label>
                </Col>
                <Col xs="12" sm="6">
                  <FormGroup check className="checkbox"> 
                      <Input className="form-check-input" readOnly={true} checked={this.state.source_sync}  type="checkbox" name="checkbox1"  name="checkbox1"  /> 
                  </FormGroup>                   
                  </Col>
              </Row>
              <Row>
                <Col xs="12" sm="6">
                <Label>object_sync</Label>
                </Col>
                <Col xs="12" sm="6">
                  <FormGroup check className="checkbox"> 
                      <Input className="form-check-input" checked={this.state.object_sync} onClick={ ((e) => this.objects())}    type="checkbox" name="checkbox1"  name="checkbox1"  /> 
                  </FormGroup>                   
                  </Col>
              </Row>
              <Row>
                <Col xs="12" sm="6">
                <Label>thumbnail_sync</Label>
                </Col>
                <Col xs="12" sm="6">
                  <FormGroup check className="checkbox"> 
                      <Input className="form-check-input" readOnly={true}  checked={this.state.thumbnail_sync}  type="checkbox" name="checkbox1"  name="checkbox1"  /> 
                  </FormGroup>                   
                  </Col>
              </Row>
               <br/> 
              <Row style={{ display: 'flex', justifyContent: 'center'}}>
                <Col xs="12" sm="2">
                    <Button color="tn-color" onClick={ ((e) => this.save())}  className="btn btn-primary">Save</Button> 
                </Col>
                <Col xs="12" sm="2">
                    <Button color="tn-color" onClick={() => this.simpleDialog.hide()}  className="btn btn-yellow">Close</Button> 
                </Col>
              </Row>
        </SkyLight>

       
      
      </div>
    )
  }
}

export default Action;