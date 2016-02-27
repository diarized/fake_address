-- DROP FUNCTION get_fake_sender(character varying,character varying);
CREATE OR REPLACE FUNCTION get_fake_sender(sender character varying, recip character varying) RETURNS RECORD
    LANGUAGE plpgsql
    AS $$
    DECLARE
        fs VARCHAR(160);
        real_recip VARCHAR(160);
        ret RECORD;
    BEGIN
        SELECT fake_sender INTO fs
        FROM fake_senders
        WHERE real_sender = sender AND recipient = recip;
        IF fs IS NULL THEN
            fs := MD5(sender || recip) || '@address.stonith.pl';
            INSERT INTO fake_senders (fake_sender, real_sender, recipient) VALUES (fs, sender, recip);
        ELSE
            UPDATE fake_senders
            SET (last_used, used_times) = (NOW(), used_times+1)
            WHERE real_sender = sender AND recipient = recip;
        END IF;
        SELECT email INTO real_recip
        FROM users, aliases
        WHERE aliases.alias = recip AND aliases.user_id = users.user_id;
        ret := (fs, real_recip);
        RETURN ret;
    END;
$$;
