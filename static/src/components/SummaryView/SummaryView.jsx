import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { Views } from '../../utils/constants';
import { Grid } from '@material-ui/core';
import { Typography } from '@material-ui/core';

export default class SummaryView extends Component {
  constructor(props) {
    super(props);
    //
  }

  componentDidMount () {
  //
  }

  render() {
    const {changeGameViewTo} = this.props;
    const summary = ["Dvir scored 0 points!"];
    const next = "millard";
    return (
      <div>
        <Grid
          container
          spacing={1}
          direction="column"
          alignItems="center"
          justify="center"
          style={{ minHeight: '50vh' }}
        >
          <Grid item xs={6}>
            <Typography color="secondary" style={{ fontSize: 25 }}>{summary}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography  style={{ fontSize: 25 }}>{next} is next!</Typography>
          </Grid>
          <Grid item xs={6}>
            <Button variant="outlined" color="secondary" onClick={() => changeGameViewTo(Views.AUDIENCE)}>Start Round!</Button>
          </Grid>
        </Grid>
      </div>
    )
  }
}

SummaryView.propTypes = {
  socket: PropTypes.any,
  changeGameViewTo: PropTypes.func,
}