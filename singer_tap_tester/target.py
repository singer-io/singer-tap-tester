"Functions to access the records that were output by the tap and validated by the target."

def get_records_from_target_output(target_output_file):
    records_by_stream = {}
    for batch in target_output_file:
        stream = batch.get('table_name')
        if stream not in records_by_stream:
            records_by_stream[stream] = {'messages': [],
                                         'schema': batch['schema'],
                                         'key_names' : batch.get('key_names'),
                                         'table_version': batch.get('table_version')}
        records_by_stream[stream]['messages'] += batch['messages']
    return records_by_stream

def examine_target_output_for_fields(target_output_file):
    fields_by_stream = defaultdict(set)
    for batch in target_output_file:
        stream = batch.get('table_name')
        for message in batch.get('messages'):
            if message['action'] == 'upsert':
                fields_by_stream[stream].update(set(message.get("data", {}).keys()))
    return fields_by_stream

def examine_target_output_file(target_output_file):
    messages_per_stream = {}
    fields_by_stream = get_records_from_target_output(target_output_file)

    return {stream: len(value['messages']) for stream, value in fields_by_stream.items() }
