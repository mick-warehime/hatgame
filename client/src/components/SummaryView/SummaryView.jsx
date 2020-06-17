import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { Views } from '../../utils/constants';

export default class SummaryView extends Component {
  constructor(props) {
    super(props);
    //
  }

  componentDidMount () {
  //
  }

  render() {
    const {boardViewChanged} = this.props;
    return (
      <div>
        <Button variant="outlined" color="secondary" onClick={() => boardViewChanged(Views.AUDIENCE)}>AUDIENCE</Button>
      </div>
    )
  }
}

SummaryView.propTypes = {
  socket: PropTypes.any,
  boardViewChanged: PropTypes.func,
}