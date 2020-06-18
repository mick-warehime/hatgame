import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { Views } from '../../utils/constants';
import { Grid } from '@material-ui/core';
import { Typography } from '@material-ui/core';

export default class AudienceView extends Component {
  constructor(props) {
    super(props);
    //
  }

  componentDidMount () {
  //
  }

  render() {
    const {boardViewChanged} = this.props;
    const message = ["Waiting for 4 players."]
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
            <Typography color="primary" style={{ fontSize: 25 }}>{message}</Typography>
          </Grid>
        </Grid>
        <Button variant="outlined" color="secondary" onClick={() => boardViewChanged(Views.ACTIVE_PLAYER)}>ACTIVE_PLAYER</Button>
      </div>
    )
  }
}

AudienceView.propTypes = {
  socket: PropTypes.any,
  boardViewChanged: PropTypes.func,
}