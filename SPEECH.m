% --- Speech Recognition + Simple AI in MATLAB 2017 ---
% Make sure you have an API key from Google Speech API
API_KEY = 'YOUR_GOOGLE_API_KEY_HERE';  % Replace with your key

% Step 1: Record speech
fs = 16000;      % Sampling frequency
nBits = 16;      % 16-bit
nChannels = 1;   % Mono
recObj = audiorecorder(fs, nBits, nChannels);

disp('Speak now...');
recordblocking(recObj, 5);   % Record 5 seconds of speech
disp('Recording finished.');

% Step 2: Save audio as WAV
y = getaudiodata(recObj);
audiowrite('speech.wav', y, fs);

% Step 3: Send audio to Google Speech API
cmd = ['curl -s -X POST -H "Content-Type: audio/l16; rate=16000" --data-binary @speech.wav ', ...
       '"https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=', API_KEY, '"'];

[status, result] = system(cmd);

if status ~= 0
    disp('Error calling Google API');
    disp(result);
    return;
end

% Step 4: Parse the JSON response
idx = strfind(result, '"transcript":');
if isempty(idx)
    disp('? Could not recognize speech.');
    return;
end
temp = result(idx+14:end);
quoteIdx = strfind(temp, '"');
userText = temp(1:quoteIdx(1)-1);

disp(['You said: ', userText]);

% Step 5: Simple AI response (rule-based)
if contains(lower(userText), 'hello')
    answer = 'Hi there! How can I help you?';
elseif contains(lower(userText), 'your name')
    answer = 'I am a MATLAB speech assistant.';
elseif contains(lower(userText), 'weather')
    answer = 'I cannot fetch weather now, but I can answer simple questions.';
elseif contains(lower(userText), 'bye')
    answer = 'Goodbye!';
else
    answer = 'Sorry, I did not understand your question.';
end

disp(['AI: ', answer]);
