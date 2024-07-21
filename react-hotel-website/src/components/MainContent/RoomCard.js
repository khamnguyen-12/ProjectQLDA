/** @jsx jsx */
import { jsx, css } from '@emotion/react';

const RoomCard = ({ room }) => {
    return (
        <div css={styles}>
            <img src={room.image} alt={room.name} />
            <div className="room-details">
                <h3>{room.name}</h3>
                <p>Loại phòng: {room.type}</p>  
                <p>Giá phòng: ${room.price} / đêm</p>
                <button>Đặt phòng</button>
            </div>
        </div>
    );
};

const styles = css`
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

    img {
        width: 100%;
        border-radius: 8px;
    }

    .room-details {
        margin-top: 12px;

        h3 {
            margin-bottom: 8px;
        }

        p {
            margin-bottom: 4px;
            font-size: 14px;
            color: #666666;
        }

        button {
            padding: 8px 16px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }
    }
`;

export default RoomCard;
