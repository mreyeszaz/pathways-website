import React from "react";
import { List, Header } from "semantic-ui-react";
export const PathwaysList = ({ pathways }) => {
  return (
    <List>
      {pathways.map((pathway) => {
        return (
          <List.Item key={pathway.title}>
            <h1>{pathway.title}</h1>
            <div>{pathway.company}</div>
            <div>{pathway.description}</div>
            <div>{pathway.image}</div>
          </List.Item>
        );
      })}
    </List>
  );
};
export default PathwaysList;
