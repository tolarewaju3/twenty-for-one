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

import {  TwitterShareButton, TwitterIcon } from 'react-share';

import {Circle} from 'react-shapes';



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
          <TableCell padding='none' align='center'>
            &nbsp;&nbsp;<Circle r={8} fill={{color:'#12c457'}} />
          </TableCell>
            <TableCell>
            <div>


             <Typography variant="h6" weight="bold"> {helper} delivered groceries to {needed_help}  </Typography>

            </div>

            <div>
                        <Typography> Austin, TX • <TimeAgo date={done_date}/>  </Typography>

            </div>

            </TableCell>

            <TableCell align='right'>
                  <TwitterShareButton url="https://www.twentyforone.com" title={helper + " delivered groceries to " + needed_help + " using Twenty for One!"} children={<TwitterIcon size={32} round={true} />} />


            </TableCell>
            
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
