def get_input(message, data_type=str):
    data = None
    while data is None:
        try:
            data = input(message + '\nUse CTRL + C to cancel.')
            if data_type == int:
                data = int(data)
            elif data_type == float:
                data = float(data)
        except (KeyboardInterrupt):
            raise KeyboardInterrupt('Input cancelled by user.')
    return data
