{
  "walls": [
    % for i, room in enumerate(rooms):
        % if i > 0:
,
        %end
    "POLYGON (({{int(room.walls[0].inner_part.point_1.x)}} {{int(room.walls[0].inner_part.point_1.y)}}\\
        % for wall in room.walls:
, {{int(wall.inner_part.point_2.x)}} {{int(wall.inner_part.point_2.y)}}\\
        % end
))"\\
    % end

  ],
  "openings": {
    "door": [
    % for i, room in enumerate(rooms):
        % if len(list(filter(lambda x: x._type == 'door', room.openings))):
            % if i > 0:
,
            %end
            % for j, op in enumerate(filter(lambda x: x._type == 'door', room.openings)):
            % if j > 0:
,
                %end
      "LINESTRING ({{int(op.placement.point_1.x)}} {{int(op.placement.point_1.y)}}, {{int(op.placement.point_2.x)}} {{int(op.placement.point_2.y)}})"\\
            % end
        % end
    % end

    ],
    "window": [
      % for i, room in enumerate(rooms):
        % if len(list(filter(lambda x: x._type == 'window', room.openings))):
            % if i > 0:
,
            %end
            % for j, op in enumerate(filter(lambda x: x._type == 'window', room.openings)):
                % if j > 0:
,
                %end
      "LINESTRING ({{int(op.placement.point_1.x)}} {{int(op.placement.point_1.y)}}, {{int(op.placement.point_2.x)}} {{int(op.placement.point_2.y)}})"\\
            % end
        % end
    % end

    ]
  },
  "furniture": {
    "bed": [],
    "cupboard": [],
    "bureau": []
  }
}