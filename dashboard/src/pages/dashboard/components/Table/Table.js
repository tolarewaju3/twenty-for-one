import React from "react";
import TimeAgo from 'react-timeago'
import {
  Table,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@material-ui/core";

// components
import { Button } from "../../../../components/Wrappers";

import { Typography } from "../../../../components/Wrappers";

import purple from '@material-ui/core/colors/purple';



const states = {
  sent: "success",
  pending: "warning",
  declined: "secondary",
};

export default function TableComponent({ data }) {
  var keys = Object.keys(data[0]).map(i => i.toUpperCase());
  keys.shift(); // delete "id" key

  return (
    <Table className="mb-0">
      <TableBody>
        {data.map(({ done_date, helper, needed_help }) => (
          <TableRow>
            <TableCell>
            {helper} delivered groceries to {needed_help}

            </TableCell>

            <TableCell>
            <a href="https://www.twitter.com">TWEET THIS</a>

            </TableCell>
            <TableCell align='right'>
              <Button
                color="success"
                size="small"
                className="px-2"
                variant="contained"
              >
                <TimeAgo date={done_date}/>
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
