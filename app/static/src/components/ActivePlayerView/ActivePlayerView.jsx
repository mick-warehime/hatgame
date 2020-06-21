import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { Views } from '../../utils/constants';
import { Grid } from '@material-ui/core';
import { Typography } from '@material-ui/core';

export default class ActivePlayerView extends Component {
  constructor(props) {
    super(props);
    //
  }

  componentDidMount () {
  //
  }

  render() {
    const {boardViewChanged} = this.props;
    const phrase = "Stone Baby"
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
            <Typography color="primary" style={{ fontSize: 35 }}>{phrase}</Typography>
            <Typography color="primary" style={{ fontSize: 45 }}>39s</Typography>
          </Grid>
          <Grid item xs={6}>
            <Button variant="outlined" color="secondary" onClick={() => boardViewChanged(Views.TEST)}>
          Got it!
            </Button>
            <Button variant="outlined" color="secondary" onClick={() => boardViewChanged(Views.TEST)}>
          Skip
            </Button>
          </Grid>
        </Grid>
      </div>
    )
  }
}

ActivePlayerView.propTypes = {
  socket: PropTypes.any,
  boardViewChanged: PropTypes.func,
}