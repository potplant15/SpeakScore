package com.speakscore.practice.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.speakscore.practice.client.*;
import com.speakscore.practice.dto.PracticeDtos.*;
import com.speakscore.practice.entity.*;
import com.speakscore.practice.repository.*;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;

@Service
public class PracticeService {
    private final PracticeRepository practices; private final EvaluationResultRepository results; private final ReferenceClient reference; private final EvaluationClient evaluation; private final ObjectMapper mapper;
    public PracticeService(PracticeRepository p,EvaluationResultRepository resultRepository,ReferenceClient referenceClient,EvaluationClient e,ObjectMapper m){practices=p;results=resultRepository;reference=referenceClient;evaluation=e;mapper=m;}
    @Transactional public Practice create(CreateRequest req){return practices.save(new Practice(req.text(),req.accent(),req.gender()));}
    @Transactional(readOnly=true) public Practice get(long id){return practices.findById(id).orElseThrow(()->new IllegalArgumentException("Practice not found: "+id));}
    public byte[] audio(long id){Practice p=get(id);return reference.synthesize(p.getReferenceText(),p.getAccent(),p.getGender());}
    public ReferenceResponse reference(long id){Practice p=get(id);return reference.pronunciationReference(p.getReferenceText(),p.getAccent());}
    @Transactional public EvaluationResult evaluate(long id,MultipartFile file){
        Practice p=get(id);p.setStatus(Practice.Status.EVALUATING);practices.save(p);
        try { EvaluationResponse r=evaluation.evaluate(p.getReferenceText(),p.getAccent(),file.getBytes(),file.getOriginalFilename()==null?"recording":file.getOriginalFilename());
            EvaluationResult result=results.findByPracticeId(id).orElseGet(()->new EvaluationResult(p));
            Double score=r.pronunciation()==null?null:r.pronunciation().score(); Double per=r.pronunciation()==null?null:r.pronunciation().phonemeErrorRate();
            result.update(r.recognizedText(),r.contentAccuracy(),r.completeness(),score,per,r.fluency(),r.overallScore(),r.wer(),r.wordsPerMinute(),r.longPauseCount(),mapper.writeValueAsString(r));
            p.setStatus(Practice.Status.EVALUATED); practices.save(p); return results.save(result);
        } catch(IOException e){p.setStatus(Practice.Status.EVALUATION_FAILED);practices.save(p);throw new IllegalStateException("Cannot read uploaded audio",e);}
          catch(RuntimeException e){p.setStatus(Practice.Status.EVALUATION_FAILED);practices.save(p);throw e;}
    }
    @Transactional(readOnly=true) public Page<Practice> list(Pageable page){return practices.findAll(page);}
    @Transactional(readOnly=true) public EvaluationResult result(long id){return results.findByPracticeId(id).orElse(null);}
}
