import moviepy.editor as mp
import speech_recognition as sr
import os, sys
#import whisper #AI

def extract_audio(video_file, audio_file):
    # Estrai l'audio dal video
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)

def transcribe_audio(audio_file, segment_duration=6, lang = "it-IT",\
                     audio_length = None):

    # Riconoscimento vocale
    recognizer = sr.Recognizer()
    timestamps = []
    idx = 0
    
    with sr.AudioFile(audio_file) as source:
        if audio_length is None:
            # Ottieni la durata totale dell'audio
            audio_length = source.DURATION  

        start_time = 0.00
        #for start_time in range(0, int(audio_length), round(segment_duration)):
        while start_time <= audio_length:    
            # Riconosci il segmento
            recognizer.pause_threshold = 3.0
            audio_segment = recognizer.record(source, duration=segment_duration)  
            #audio_segment = recognizer.adjust_for_ambient_noise(source, duration=segment_duration)
            try:
                # Riconosci il parlato
                text = recognizer.recognize_google(audio_segment, language=lang)
                print(f"Testo: {start_time} secondi: {text}")

                # Aggiungi il timestamp e il testo
                if idx:
                    timestamps[idx-1][1] = start_time - 0.1

                timestamps.append([])
                timestamps[idx].append(start_time)
                timestamps[idx].append(0.0)
                timestamps[idx].append(text)
                idx += 1

                #timestamps.append((start_time, 0, text))

            except sr.UnknownValueError:
                #print(f"Audio non riconosciuto da {start_time} secondi")
                pass

            except sr.RequestError as e:
                #print(f"Errore nella richiesta a Google Speech Recognition: {e}")
                pass

            start_time += segment_duration

    return timestamps

def save_timestamps(timestamps, output_file):
        '''
        0
        00:00:00,000 --> 00:00:02,000
        Subtitles created using Matesub

        '''
        nn = 0
        with open(output_file, 'w') as f:
            for start_time, fine_time, text in timestamps:
                nn += 1
                hours = start_time // 3600
                minutes = (start_time % 3600) // 60
                seconds = start_time % 60
                hours1 = fine_time // 3600
                minutes1 = (fine_time % 3600) // 60
                seconds1 = fine_time % 60

                f.write(f"\n{nn}\n{hours:02}:{minutes:02}:{seconds:02} --> {hours1:02}:{minutes1:02}:{seconds1:02}\n{text}\n")

def main(video_file, blocco, lingua):
     
    af = video_file.split('mp4')    #"audio.wav"
    audio_file = af[0] + 'wav'
    output_file = af[0] + 'srt'  #"timestamps.txt"

    #extract_audio(video_file, audio_file)
    timestamps = transcribe_audio(audio_file, blocco, lingua)
    save_timestamps(timestamps, output_file)

    # Rimuovi il file audio temporaneo
    #os.remove(audio_file)

if __name__ == "__main__":


    lingua = 'it-IT'
    p1 = 'Errore' 
    p2 = ''
    
    if len(sys.argv) > 2:

        try:
            p1, video_file = sys.argv[1].split('=')
        except:
            p1 = 'Errore'
        
        try:
            p2, blocco = sys.argv[2].split('=')
        except:
            p1 = 'Errore'

        if len(sys.argv) ==4:
            try:
                p3, lingua = sys.argv[3].split('=')
            except:
                p1 = 'Errore'

        #str(sys.argv[1]), video_file   
        if p1 == 'video' and p2 == 'blocco':
            #video_file = '/home/rosa/Video/IfiglidiDune3min.mp4'
            main(video_file, float(blocco), lingua)
        else:
            p1 = 'Errore'

    if p1 == 'Errore':
        print(sys.argv[0] +" "+ sys.argv[1] +" "+ sys.argv[2] +'\n'+\
              "Controllare parametrimancanti video e range di scansione\n"\
              "video=?.mp4\n"\
              "blocco=secondi\n")
             
        ''' \ "lingua=en-EN se mancante 'Italiano'") '''
